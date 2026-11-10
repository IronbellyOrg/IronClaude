review: 1 of 3

# Audit: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (first review of the whole document)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate sha256: `89aa60a626c2210c7e3cd02a711923cbaf3990a333b6398f744d27073b0d61ba` (285 lines, 58012 bytes)
- Baseline: none given, none needed (first review). Prior report: none.
- Reviewer model: Sonnet 5.5 (claude-sonnet-5-5)
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full). Mode, Review Loop and Mandatory Output Artifacts per `command.md:121-123, 256-264, 307-343`.
- Coverage: the whole candidate, read in full. Evidence checked: `README.md` (all), the three inventories (the lines the spec cites for its load-bearing claims, spot-checked: INV-A:3,13-17,62,65,66,73-120; INV-B:36,46,52,109-112,207-215,272,279-323; CAPS:44-47,52,58,64-67,72-80,86,92,97-103,115-116,129-130,145-161,178-188). Everything under `src/`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/` and `~/.claude/{commands,skills}` is not in the sandbox, so a citation that points there and is not quoted by an inventory is UNVERIFIED. Not covered: the other 285-line-spec claims that only an out-of-sandbox file can settle (listed at the end).
- Process note: one directory listing of `~/.claude` was run before the sandbox home was confirmed (names only, nothing read or written outside the sandbox).

## Summary
The decision (section 1) is well argued, the counts reconcile (10 + 27 + 6 = 43; INV-A 5/13/3 plus INV-B 5/14/3), every section-3 row maps to exactly one phase, and the stated evidence gaps (spec:42-45) are honest. One blocking finding: the P1 scope and its acceptance test contradict the per-row phasing, the "None" fixes of two ready commands, and open decision D3. Six Medium findings and several notes are listed under follow-up candidates.

## === REQUIREMENTS ANALYSIS === (Wiegers lead, Adzic, Cockburn)

### Finding R-1 (MAJOR, blocking) - P1 scope and AC-1.1 cannot be met together with the rest of the document
- Experts: Wiegers (consistency), Whittaker (Sequence Attack).
- Stated texts that contradict each other:
  1. Spec:159 (P1): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except load (B-2) (a no-op where a command has no gate)".
  2. Spec:195 (AC-1.1): the P1 test "asserts that every command in sections 3.1-3.2 except load (B-2) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one".
  3. Spec:79 (3.1 lead-in): "The only command changes are the small fixes in the last column"; spec:84 (brainstorm) and spec:87 (init-lite) give "None" and no phase.
  4. Spec:76: only "changed" commands gain the section. Spec:99-125 give the gate resolutions of 27 commands to P2, P3 and P4 (for example spec:104 cli-eval, spec:109 implement, spec:114 pr-submit).
  5. Spec:154 and spec:162: Phase 4 "waits for answers to D2-D4"; spec:240 (D3 option a, recommended): pr-submit is run by the coordinator or person and there are "no pr-submit changes in Phase 4"; spec:139 says pr-submit stays a worker candidate "only if the user accepts D3".
- Sentence: An implementer who follows the stated text as written builds, in P1, a flag and an `## Unattended mode` section on brainstorm, init-lite, implement, post-release and pr-submit (and on every P2 and P3 command), and builds the AC-1.1 test to require them. This is wrong because (a) brainstorm and init-lite are stated to need no change (spec:84, 87, 79); (b) implement, post-release and pr-submit would carry a section before the user decisions D2-D4 that spec:154 says gate them, and, under the recommended D3(a), pr-submit would carry a worker section although it is to stay coordinator-run; (c) P2-P4 commands would accept `--unattended` in P1 while their gate resolutions arrive only in P2-P4, so a command such as `/sc:cleanup --unattended` still prompts between phases (spec:103 vs 159) and AC-1.1 passes on a command that still stalls. The phase gate "Later phases do not start until the earlier phase's checks pass" (spec:154) makes the test unpassable or meaningless as written.
- Recommendation: narrow P1 and AC-1.1 to the P1 commands in spec:159 (the nine named plus the four small fixes), and let each later phase add its own commands to the test (spec:199 already does this for gates). Delete "every command in sections 3.1 and 3.2" from spec:159 and spec:195, or state that brainstorm and init-lite get the section in P1 and drop "None" from spec:84, 87.
- Priority: High. Quality impact: removes an unpassable gate and a hidden decision bypass.

## === ARCHITECTURE ANALYSIS === (Fowler lead, Newman, Hohpe, Nygard)

The architecture is coherent: one coordinator, one top-level worker per command, one shared contract file, no Orca calls in commands (spec:16, 29-37, 213). The depth-1 argument (spec:33) is correctly caveated (CAPS:103). Boundaries between the contract file (WC-1..12), per-command sections and coordinator duties (spec:72-73) are clear. Findings below are all Medium or minor, so none triggers a revision.

## Follow-up candidates (Medium findings and minor notes; none blocks, none enters the Reviser brief)

### M-1 (Medium; MAJOR label) - Retry safety has no owner (Wiegers, Nygard)
- Spec:64 (WC-6): a command with no resume flag "writes each run into a fresh output directory so a re-run starts clean", and spec:99-125 mark most rows "fresh dir". But the output directory is passed by the coordinator (spec:62 WC-4, spec:73 section 2.3), and section 2.3 does not say the coordinator must pass a new directory on a `--retry-of` start. If the retry brief repeats the first brief, the retry overwrites the first attempt's report and contract. It needs a guess about what the coordinator passes, so Medium. Recommendation: add one line to 2.3: a retry brief names a new output directory.

### M-2 (Medium) - Reflect and tasklist unattended behaviour departs from the inventories without new evidence (Nygard, Whittaker)
- Spec:88 makes `--remediate` under `--unattended` follow the headless auto-accept rule; spec:122 makes tasklist Stage 10.5 pass `--unattended` to every reflect so that rule applies. INV-B:109 says that rule "auto-accepts for auto-fixable registers and skips the gates"; INV-B:215 recommends instead that Stage 10.5 call reflect without `--remediate` and run the reflect fan-out at the worker's top level. The spec's verdict that reflect is "ready" (spec:88) and its answer to INV-B:215 ("inside Claude Code's nesting limit, INV-A:14", spec:122) are asserted, not traced: tasklist worker, reflect agent, reflect Tier 2 reviewers and adversarial advocates are up to four layers against a documented three (INV-A:14). Which gates the headless rule skips is not stated. Recommendation: either adopt INV-B:215 for the unattended path or cite the lines that show the depth and the skipped gates. UNVERIFIED (`sk/sc-reflect-protocol/refs/remediation-handoff.md:239-247`, `sk/sc-tasklist-protocol/SKILL.md:1614-1631` not in sandbox).

### M-3 (Medium) - AC-C1 may fail on the spec's own P0 deliverables (Wiegers, Whittaker)
- Spec:172 (AC-C1) requires no match of `orca(-ide) orchestration|worktree|terminal|agent` under `src/superclaude/core` (and commands, skills, agents). Spec:158 (P0) requires a new `WORKER-CONTRACT.md` in `src/superclaude/core` with a coordinator brief template and a new Orca section in `HOW-WE-WORK.md` (also under core; spec:25 E5 says it has zero Orca mentions today), and spec:61 (WC-3) and spec:147 (SA-2) expect the contract file to name the preamble's `ask` command as an example. A natural text such as "`orca orchestration ask`" matches AC-C1. SA-2 (spec:147) speaks of command, skill and agent files only, AC-C1 also scans core. Recommendation: exclude `WORKER-CONTRACT.md` and `HOW-WE-WORK.md` from AC-C1, or forbid command strings in them.

### M-4 (Medium) - cli-eval wait splitting is not gated or listed as an allowed edit (Wiegers)
- Spec:104 requires cli-eval to "split the eval wait into waits of at most 4 minutes" and spec:160 files it under P2. Spec:148-149 (SA-3, SA-4) require standalone behaviour unchanged and allow existing-line edits only for the listed defect fixes (cli-eval is not listed), and AC-C5 (spec:176) fails on any removed line. The row does not say the split applies only under `--unattended`. Recommendation: say it is an added unattended-only paragraph, or add it to the SA-4 list.

### M-5 (Medium) - Existing contracts' `status` vocabulary is unchecked (Adzic)
- Spec:62 (WC-4) says commands with a contract "keep their fields and add the missing ones", and 7.2 step 4 (spec:183) asserts `status` in the four-value set for every P1 command. INV-B:272 lists a `status` field for workflow, but no inventory line states the values used by workflow, reflect, brainstorm or adversarial. If they differ, keeping them cannot satisfy the assertion. Recommendation: say which wins, or cite the existing values. UNVERIFIED (`sk/sc-workflow-protocol/refs/return-contract.md:3-19`).

### M-6 (Medium) - Blocked and failed look the same to Orca (Hohpe)
- Spec:63 (WC-5) sends `--outcome failed` for both `failed` and `blocked`; the coordinator can tell them apart only by opening the file (spec:62, 73). AC-2.2 (spec:200) relies on the file. Not wrong, but a coordinator that reads only the Orca outcome will retry a blocked Task, and the circuit breaker (CAPS:80 shows only the worker's own `failed` report does not count) leaves retry unlimited by Orca. Recommendation: require the first body sentence to start with `blocked:` (spec:63 already requires the status in the first sentence) and tell the coordinator not to `--retry-of` a blocked Task without a new answer.

### Minor notes
- N-1: spec:44 says a command question "does not fail `worker-start`", which narrows README.md:13 ("a supervised Claude worker that waits on a question fails Orca's 60-second readiness limit"). CAPS:47 supports the reading (readiness waits for the composer before the task is typed), but the sentence is a derived claim; AC-0.4 does test it, so keep it labelled as derived.
- N-2: the adversarial contract path `<output>/adversarial/return-contract.yaml` (spec:83) differs from the general WC-4 rule `<output-dir>/return-contract.yaml` (spec:62); say so in WC-4.
- N-3: pr-submit's top-level rule is cited at `SKILL.md:37-39` (spec:11, 65, 114; INV-A:10, INV-B:90) but CAPS:161 cites the installed copy at lines 47-49. Different copies, not a conflict; name the copy once.
- N-4: spec:285 (UNVERIFIED item 14) and the header (spec:3) carry process history (task id, validator run) that is not requirement text; harmless.
- N-5: E5 (spec:25) and AC-C1 rely on a grep "run 2026-11-02" that the reader cannot repeat from the inventories; re-run it in P0.

## Guard Condition Boundary Table (triggered: the spec contains numeric thresholds and boolean guards)
Responsibility: Nygard (construction), Crispin (completeness), Whittaker (attack). Classes left out are given one line.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| nesting depth fence | spec:33 (R1) | Typical | depth 1, worker calls `worker-start` | refused `nested_worker_depth_exceeded` | refused; call sites presumed, `task-create` UNVERIFIED (CAPS:103) | OK (caveated) |
| nesting depth fence | spec:66 (WC-8) | Legitimate edge | depth raised (D5 b) | fence off | WC-8 still forbids the call | OK |
| readiness limit | spec:59 (WC-1) | Maximum/Overflow | fallback above ~45 s | fails | stated (EVIDENCE.md:56, UNVERIFIED here) | OK |
| heartbeat cadence | spec:68 (WC-10) | Typical | wait <= 4 min | heartbeat possible | split into <= 4 min waits | OK |
| heartbeat cadence | spec:68 (WC-10) | Maximum/Overflow | single tool call > 5 min | no heartbeat | commands must split; pr-submit shown per iteration; poll runtime UNVERIFIED (spec:283 item 12) | OK (caveated) |
| heartbeat cadence | spec:68 (WC-10) | Zero/Empty | no wait at all | n/a | n/a; class cannot occur | OK |
| outcome mapping | spec:63 (WC-5) | Sentinel Value Match | `partial` | maps to succeeded | stated, body must say partial | OK |
| outcome mapping | spec:63 (WC-5) | Sentinel Value Match | `blocked` | maps to failed | stated; indistinguishable from `failed` at Orca level | GAP (Medium, M-6) |
| outcome mapping | spec:63 (WC-5) | Zero/Empty | no report file | maps to failed | stated | OK |
| contract status set | spec:62, 183 | Legitimate edge | existing contract with another `status` value | assertion fails | unspecified which wins | GAP (Medium, M-5) |
| output directory | spec:64 (WC-6), 73 | One/Minimal | retry reuses the first brief's directory | overwrite | unspecified | GAP (Medium, M-1) |
| unattended switch | spec:51, 228 (D1) | Sentinel Value Match | token `--unattended` inside quoted content | not a flag | decided only in the spec-panel command text, not in WC-2 | OK for this audit (the command defines it) |
| confidence threshold | spec:121 (task) | Maximum/Overflow | exactly 0.70 | below-0.70 rule does not fire | inventory-level behaviour not restated | OK (inherited) |
| `--monitor` ordinal | spec:114 (pr-submit) | Legitimate edge | `--monitor 1` | refused | stated | OK |
| P1 flag acceptance | spec:159, 195 | Legitimate edge | command with a gate (cleanup) | flag accepted, gate still fires | contradicts spec:103 | GAP (blocking, R-1) |

The GAP rows in M-1, M-5 and M-6 name no wrong outcome without a guess, so they are Medium (FR-8/FR-9 grading, command.md:332-333). The R-1 row names the concrete outcome above.

## Whittaker attacks (Sequence and Divergence)
- Sequence Attack on section 6: the invariant at spec:154 ("later phases do not start until the earlier phase's checks pass") fails when AC-1.1 (spec:195) demands content the later phases create. Concrete attack: P1 finishes with 9 commands edited; the AC-1.1 test lists 36 commands; 27 lack the section; the gate never opens (finding R-1).
- Divergence Attack on D3: with D3(a) chosen, spec:114 (pr-submit worker row) and spec:195 conflict (same finding).
- Pipeline Dimensional Analysis: not triggered (no multi-stage data pipeline with count changes). Correctness focus not requested, so no State Variable Registry.

## Reviser brief
Blocking finding ids: R-1.
Rules for the reviser (restating command.md:263): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings (M-1 to M-6, N-1 to N-5) alone.

## UNVERIFIED items in this audit
- All `src/superclaude/...`, `CLAUDE.md:N`, `HOW-WE-WORK.md:N`, `install_core.py:N`, `pyproject.toml:38`, `Makefile:68-74`, `EVIDENCE.md:N` and `.dev/codegraph-migration/...` citations in the candidate that are not quoted by an inventory line.
- The statement that 11 locations were re-read (spec:11) and the 340-citation check (spec:285).

verdict: FAIL

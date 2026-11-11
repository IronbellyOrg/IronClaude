review: 1 of 3

# Spec-panel critique, round 1

## Run metadata
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Command: `/sc:spec-panel --mode critique --focus requirements,architecture` (first review of the full document; no `--re-review`, no `--baseline`, so no baseline note is needed beyond this line).
- Panel (command.md:99-113 order, selected by focus plus the always-on adversarial expert at command.md:83): Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Newman, Hohpe (architecture); Whittaker. Crispin, Gregory and Hightower are not selected by these focus areas.
- Inputs read in full: the README (`README.md:1-38`), the spec, `inventory/commands-a.md` (120 lines), `inventory/commands-b.md` (323 lines), `inventory/orca-capabilities.md` (188 lines). No input was missing or unreadable.
- Citation convention in this report: `S:N` = line N of the spec, `INV-A:N` / `INV-B:N` / `CAPS:N` = lines of the three inventories, `CMD:N` = `command.md` in the run folder.
- Not available in the sandbox, so every claim that depends on them is UNVERIFIED: `src/superclaude/**`, `CLAUDE.md`, `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, `.dev/codegraph-migration/**`, `orca-ide` output, `~/.claude/WORKER-CONTRACT.md` (nothing exists under the sandbox home), `~/.claude/agents/rf-qa.md`.

## Result at a glance
- Blocking findings: 0. The 14 findings below (F-1 to F-14) were each put through the grading sentence; none holds without a further assumption, so all are Medium and are listed under follow-up candidates.
- Grading note on FR-8 / FR-9. The Guard Condition Boundary Table below has 13 GAP rows. The command text (CMD:259, CMD:328-329) calls FR-8/FR-9 findings blocking. The brief's grading check says a finding that is a requirement the document never states is Medium even when labelled MAJOR. I applied the brief's check to every FR-8 finding (each GAP row maps to a finding F-n with its own sentence) and I am recording the conflict here so the coordinator can overrule it. If the coordinator reads CMD:259 as overriding the brief, the verdict flips to FAIL on F-1, F-2, F-3, F-4, F-5, F-7, F-8 and F-9 (the findings that carry a GAP row).
- The candidate's central decision (Orca coordinates, commands stay the units of work, section 1) is supported by the inventories as far as they can be checked, and the spec states its own evidence gaps (S:42-45). I found no stated text that causes data loss or breaks a security boundary.
- The panel advisory-recommends `--focus correctness` for a follow-up pass: the spec has numeric thresholds (60 s, 5 min, 4 min, 240 s, 0.70 via the task row) and a status-to-outcome mapping (CMD:192).

## Quality scores (0-10)
Clarity 7, Completeness 6, Testability 6, Consistency 6.

## === REQUIREMENTS ANALYSIS ===

**Wiegers (lead).** Most requirements carry owner, evidence and a testable check (WC-1..WC-12, S:59-70; AC blocks S:172-210). The weak spots are places where a requirement refers to something the spec does not define: the directory in WC-4 (F-1, F-2), "fresh output directory" in WC-6 (F-3), the four-value `status` set against existing contracts (F-8), and the token that turns the mode on (F-7).

**Adzic.** Example run for F-1. Given `/sc:tdd "auth" --unattended --output docs/auth/TDD_AUTH.md` and a bare topic. When the command resolves the gate as blocked (S:90). Then WC-4 (S:62) says the contract is `<output-dir>/return-contract.yaml` where `<output-dir>` is "the directory the coordinator passed". The coordinator passed a file. Before state: no TDD file. After state: undefined. Degenerate variant: `--unattended` with no `--output` at all (F-2).

**Cockburn.** Actors are well named: coordinator, worker session, command (S:57, S:72-73). Gap in the goal chain: the actor who must make an output directory unique per attempt is not named (F-3), and the actor who decides a command is "dispatchable yet" is not named (F-6).

### F-1 File-valued `--output` against the directory in WC-4 [MAJOR label, graded Medium]
- Issue: WC-4 defines `<output-dir>` as the directory passed with `--output` / `--output-dir` (S:62). Section 3.1 tells the brief to pass `--output <file>` for tdd (S:90, INV-B:47 "TDD file at `--output`") and init-lite (S:87, INV-A:55), section 3.2 adds `--output` for spec-panel, whose product is a review document (S:120, INV-B:182), and AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` (S:200). Section 7.2 step 4 needs a `<contract>` path (S:183). The run's own command definition resolves the same problem with a separate directory flag and says "`--output` is file-valued" (CMD:456).
- Grading sentence: An implementer who follows WC-4 as written for tdd builds the contract at `<the --output value>/return-contract.yaml`, i.e. under the TDD file path; that is wrong because on a blocked run it creates a directory named like the TDD file, which the later successful re-invocation (WC-3, S:61) cannot write its TDD into. Why Medium: the implementer can equally take the parent directory of the file; the text allows both.
- Expert: Wiegers, Fowler. Recommendation: define one directory-valued flag for the contract (or say "dirname of a file-valued `--output`") and restate AC-2.2 with it. Priority: High. Quality impact: Testability +1, Consistency +1.

### F-2 No rule for a missing or unusable output directory [MAJOR label, graded Medium]
- Issue: WC-4 says the report is "known before dispatch" and "written on every outcome ... including stops before any other output exists" (S:62), but several rows give the command no brief-supplied directory: research ("contract naming the generated `claudedocs/research_*.md` path", S:116; file name generated at run time, INV-B:132; no output flag), workflow (`.dev/tasks/to-do/<id>/`, id generated, brief passes only `--handoff none`, S:92), troubleshoot (timestamped default directory, INV-B:242). Nothing says what a command does under `--unattended` when no directory is passed, or when it cannot be created or written (for example inside `.git/`). Unwritable directory is exactly the case where "written on every outcome" cannot hold.
- Grading sentence: An implementer who follows WC-4 for research builds a command that writes a contract at a location the coordinator cannot know before dispatch, which is wrong because WC-4's own title requires the path known before dispatch; the text never states the fallback. Medium: a requirement the document never states.
- Expert: Wiegers, Nygard. Recommendation: one general rule: under `--unattended` with no resolvable writable directory the command refuses before any work and prints the refusal in chat only (CMD:456 is a precedent), and every command row lists how the directory is passed. Priority: High.

### F-8 Contract `status` vocabulary and the undefined `partial` [MAJOR label, graded Medium]
- Issue: WC-4 fixes `status` to `succeeded|partial|failed|blocked` and also says commands that already write a contract "keep their fields" (S:62). The inventories show existing contracts (workflow contract 1.1, INV-B:272; adversarial, INV-A:35; reflect, INV-B:112; brainstorm, INV-A:39) but not their `status` values, so a collision with the four-value set is UNVERIFIED. `partial` maps to `--outcome succeeded` (S:63, S:263) and is never defined: when a run is partial rather than failed is not stated, yet a settled-succeeded Task makes dependents startable (CAPS:89-90).
- Grading sentence: An implementer who follows WC-4 and WC-5 as written for a command whose existing contract already has a different `status` set builds either two meanings of `status` or a renamed field, and that is wrong because "keep their fields" and "one of four" cannot both hold; I cannot show the existing vocabularies, so this needs a guess. Medium.
- Expert: Wiegers, Newman. Recommendation: define `partial` in one sentence, state per existing contract how its status maps, and give the contract a version field (see N-11). Priority: Medium.

### F-9 Readiness claim stated as fact, not listed as UNVERIFIED [MAJOR label, graded Medium]
- Issue: S:44 says a command's own question "comes *after* readiness, so it does not fail `worker-start`", citing CAPS:52 and CAPS:129. Those lines say a worker already at `input_accepted` that waits is healthy (CAPS:52). For Claude the task is passed on the command line (CAPS:47), so the command can begin as Claude launches, and the spec shows no evidence about the order between composer-ready and a first-action question. The item is absent from the UNVERIFIED list (S:271-285), and the P0 smoke runs (S:158, S:194) contain no command that asks at its first action. WC-1's "well inside" is also unquantified (S:59).
- Grading sentence: An implementer who follows S:44 concludes gate stalls only happen after start and adds no start-time protection for first-action gates (tdd bare topic, cli-eval suite menu, review-translation Phase 1, S:90, S:104, S:117); that is wrong if such a question blocks the composer, because `worker-start` then fails at `agent_readiness` and leaves a terminal to reclaim (CAPS:112). It needs the guess that the order is the worse one. Medium.
- Expert: Nygard, Whittaker. Recommendation: move the claim to UNVERIFIED and add one first-action-gate command to the P0 smoke set. Priority: Medium.

## === ARCHITECTURE ANALYSIS ===

**Fowler (lead).** The boundary is clean: commands hold no Orca calls (WC-8, SA-2), the coordinator holds the Task DAG, the contract file is the interface. The interface is shared across 37 commands through one core document, which is the right place (S:52). Weak points: the interface path is not uniform (F-1, F-2, and the adversarial and workflow rows give paths that differ from WC-4: S:83, S:92), and the interim state between phases is not controlled (F-6).

**Nygard.** Failure modes considered: worker dies with no `worker_done` and no contract (the spec leans on Orca liveness verdicts, CAPS:120-129, and says only that the coordinator sees `agentWait` or a missing report, S:44; acceptable as Orca's guide governs recovery, noted as N-8); a blocked gate (covered, WC-2/WC-3); retry (F-3); long waits (F-4, F-5); concurrent edits (F-11).

**Newman.** The contract has no schema version (workflow's contract is versioned 1.1, INV-B:272) while 37 commands will emit it and a coordinator will parse all of them; evolution is unmanaged (N-11).

**Hohpe.** Message pattern is sound: one `worker_done` from the dispatched pane (WC-5, WC-7), `ask` resumed by message ID (WC-3), `check` pulled (WC-12). One ordering rule is implied but not written: the contract file must be complete before `worker_done` carries its path (S:62, S:63). Low risk; noted in N-11.

### F-3 "Fresh output directory" against a path fixed before dispatch [MAJOR label, graded Medium]
- Issue: WC-6 says a command with no resume flag "writes each run into a fresh output directory so a re-run starts clean" (S:64), and most section 3.2 rows say "fresh dir". WC-4 fixes the contract at `<output-dir>/return-contract.yaml` before dispatch (S:62), and section 2.3 (S:73) lists what the coordinator passes (command line, output directory, authorizations, placement) without saying "a new directory per attempt". A `worker-start --retry-of` worker (CAPS:116) given the same brief writes into the same directory.
- Grading sentence: An implementer who follows WC-4 and WC-6 builds commands that write straight into the directory in the brief; a retry with that same brief overwrites the first attempt's contract and outputs, which is the corruption WC-6 forbids. Medium: the text allows the reading that the coordinator supplies a new directory, and the reading that the command creates a subdirectory (which would move the contract path).
- Expert: Nygard, Whittaker (Sequence attack: repeat step). Recommendation: put one sentence in section 2.3: new output directory per attempt, chosen by the coordinator; commands never append a subdirectory. Priority: High.

### F-4 WC-10 reaches every long Agent-tool wait but only two commands are handled [MAJOR label, graded Medium]
- Issue: WC-10 applies to "a command step that blocks a single tool call for longer than 5 minutes" (S:68). Fan-out commands block in foreground Agent-tool calls: adversarial Mode B (INV-A:35), cleanup-audit waves of 7-8 agents (INV-A:42), tdd (INV-B:221), troubleshoot Tier 2 (INV-B:241). The examples in WC-10 and the rows that carry it are cli-eval and pr-submit only (S:104, S:114); AC-4.3 tests only pr-submit (S:210). Whether Orca uses heartbeat age in liveness is itself UNVERIFIED (CAPS:130, CAPS:182), and the spec does not list it.
- Grading sentence: An implementer who follows WC-10 as written splits waits in cli-eval and pr-submit and leaves the other fan-out commands unsplit, which is wrong because the same sentence requires every such step to be split; or tries to split a foreground Agent call, which the command cannot do. Medium: the text does not say whether Agent-tool waits are in scope.
- Expert: Nygard. Recommendation: scope WC-10 to polling and sleep waits, or state that a foreground Agent-tool wait is exempt, and add heartbeat-age effect to UNVERIFIED. Priority: Medium.

### F-5 pr-submit poll interval has no upper bound; AC-4.3 is stricter than WC-10 [MAJOR label, graded Medium]
- Issue: the pr-submit row relies on "poll then a sleep of at least `--poll-interval`" with each iteration under 4 minutes (S:68, S:114) but sets no cap on `--poll-interval`; its poll-script runtime is UNVERIFIED (S:283). WC-10 splits only calls "longer than 5 minutes" (S:68) while AC-4.3 fails any call over 240 s (S:210), so a 250 s call passes the requirement and fails the check.
- Grading sentence: An implementer who follows the pr-submit row builds a loop whose sleep equals the configured interval; with `--poll-interval 300` one sleep exceeds 240 s and AC-4.3 fails, and the text lets that value through. Medium: depends on the interval chosen.
- Expert: Whittaker (Accumulation / boundary), Nygard. Recommendation: cap the interval at 240 s under `--unattended` and make WC-10 and AC-4.3 use the same number. Priority: Low.

### F-6 Flag-everywhere in P1 versus gates converted in P2-P4 [MAJOR label, graded Medium]
- Issue: P1 adds "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" and AC-1.1 requires an `## Unattended mode` section for all of them (S:159, S:195). The gate behaviour of 15 commands arrives in P2, of 4 in P3, and of implement, post-release and pr-submit in P4 after decisions D2-D4 (S:160-162, S:154). Between phases the flag is accepted but WC-2 and WC-9 are not yet true. D3(a) recommends pr-submit stays with the coordinator and receives "no pr-submit changes" (S:240), yet AC-1.1 gives it a section in P1.
- Grading sentence: An implementer who follows P1 builds `--unattended` into auggie-review while its default still posts to GitHub with no prompt (S:100, INV-A:38); that is wrong because WC-9 says `--unattended` turns such defaults off (S:67). It needs the guess that someone dispatches that command before P2; the spec never forbids it.
- Expert: Fowler, Newman, Cockburn. Recommendation: either limit P1 flag acceptance to commands that have no gate, or make an unconverted command refuse `--unattended` as blocked; add to section 2.3 that a command is dispatchable only after its phase check passes; exempt the P4 commands from AC-1.1. Priority: High.

### F-7 How the mode is detected, and what person-mode flags do under it [MAJOR label, graded Medium]
- Issue: D1(a) sells the flag as "testable by grep and cannot misfire on a person" (S:228) but states no token rule. A quoted topic containing the text `--unattended` (for example `/sc:troubleshoot "why does --unattended fail"`) would switch mode if detection is a substring match; the run's own command definition adds the rule "standalone argument token outside any quoted argument" (CMD:455). Person-mode flags are refused for some commands (cleanup, improve, roadmap, test, explain, pr-submit, business-panel) but for adversarial, brainstorm and release-split the spec only says the brief must never pass `--interactive` (S:83, S:84, S:89), so `--unattended --interactive` on those is unspecified. Section 4 says coordinator-only commands "get no `--unattended` mode" (S:128) and does not say what happens if one receives it.
- Grading sentence: An implementer who follows D1 as written builds substring detection for `--unattended`, which is wrong for a quoted topic because it silently drops approval gates the person expected; it needs the guess that substring detection is chosen. Medium.
- Expert: Whittaker (Sentinel collision, Divergence). Recommendation: copy the token rule into WORKER-CONTRACT.md and add one general rule: under `--unattended`, any person-mode flag resolves as blocked. Priority: Medium.

### F-11 Concurrent edits to the same source files [MAJOR label, graded Medium]
- Issue: WC-11 forbids two workers writing the same file but its remedy covers only default output paths and single-owner memory keys (S:69). Workers share the current worktree by default (CAPS:115, quoted at S:69). Commands that edit product files (implement INV-A:51, improve INV-A:52, cleanup INV-A:43, document inline INV-A:47, test `--fix` INV-B:48) cannot enforce this themselves, and section 2.3 (S:73) does not make the coordinator partition files or pick separate worktrees.
- Grading sentence: An implementer who follows WC-11 builds unique output paths and nothing else, which is wrong for two editing workers on one file because the later write silently replaces the earlier edit. Medium: a requirement the document never states, and the coordinator may already do this.
- Expert: Nygard, Fowler. Recommendation: add to section 2.3 that editing Tasks run on disjoint files or in separate worktrees. Priority: Medium.

### F-13 Availability of the shared contract file, and AC-C1 against P0 [MAJOR label, graded Medium]
- Issue: each changed command points at `~/.claude/WORKER-CONTRACT.md` (S:52) and that file is installed only by `superclaude install` after the name joins `KNOWN_CORE_FILES` (S:52, S:158). The spec gives no behaviour when the file is missing or unreadable (a dev checkout before reinstall, or a project where an older install ran), and `make verify-sync` (S:173) does not cover core files; the repo's dual-surface lookup rule for primitives is in `CLAUDE.md`, not in the workspace, so whether it applies is UNVERIFIED. Separately, AC-C1 greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` and requires no output (S:172), while P0 adds an Orca section to HOW-WE-WORK.md and a contract file in that folder (S:158) and SA-2 allows an Orca mention in the contract file (S:147).
- Grading sentence: An implementer who follows P0 and AC-C1 writes a routing section or brief template that names `orca orchestration ...`, and AC-C1 then fails on the spec's own deliverable; it needs the guess that the text uses the literal command names. Medium.
- Expert: Fowler, Newman. Recommendation: state "unreadable contract file under `--unattended` resolves as blocked", and narrow AC-C1 to commands, skills and agents, or exempt the two P0 files by name. Priority: Medium.

### F-14 tasklist passes `--unattended` to reflect, which changes remediation behaviour [MAJOR label, graded Medium]
- Issue: the inventory recommended that Stage 10.5 call reflect without `--remediate` (INV-B:215). The spec instead keeps `--remediate` and passes `--unattended`, so reflect's headless auto-accept rule decides (S:122, S:88). The headless rule "auto-accepts for auto-fixable registers and skips the gates" (INV-B:109); what the auto-accept then runs (sc:workflow or task-builder) and that it happens in N subagents is not described, and who answers the offer inside subagents is UNVERIFIED (INV-B:322). WC-9 (S:67) lists only outward actions, so this auto-remediation is neither authorized nor forbidden by the brief.
- Grading sentence: An implementer who follows the tasklist row builds a run that, under `--unattended`, starts remediation handoffs in every phase without the brief asking for them; that is wrong if the coordinator expected a plain generation run. `--no-reflect` exists (S:122) so the coordinator can avoid it; Medium.
- Expert: Fowler, Nygard. Recommendation: under `--unattended` make Stage 10.5 run reflect without `--remediate`, as the inventory advised, or state what the auto-accept performs. Priority: Medium.

## === ADVERSARIAL ANALYSIS (Whittaker) ===
Format per the command (CMD:82): attack, invariant location, trigger, trace. All results below are mapped to the findings above; none escapes the Medium grade.

1. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (S:62), "written on every outcome"** fails when **`--unattended` is passed with no output directory**. Concrete attack: `/sc:research "x" --unattended`; before: no directory known; after: no contract, `worker_done --outcome failed` by WC-5 with nothing for the coordinator to read. Maps to F-2.
2. I can break this specification by **Divergence Attack**. The invariant at **WC-4 `<output-dir>` (S:62) against tdd/init-lite `--output <file>` (S:87, S:90)** fails when **the passed value is a file**. Trace: blocked run creates `TDD_AUTH.md/return-contract.yaml`; retry writes `TDD_AUTH.md` as a file: path collision. Maps to F-1.
3. I can break this specification by **Sentinel Collision Attack**. The invariant at **D1 (S:228)** fails when **quoted topic text contains `--unattended`**. Trace: person-intended interactive run drops its approval prompts. Maps to F-7.
4. I can break this specification by **Sequence Attack**. The invariant at **WC-6 (S:64)** fails when **the same brief is dispatched twice with `--retry-of`**. Trace: attempt 1 writes contract (`failed`) and artifacts to `dir/`; attempt 2 starts, writes into `dir/` first thing, overwriting the contract with `blocked`/partial content before finishing. Maps to F-3.
5. I can break this specification by **Sequence Attack**. The invariant at **P1/P2 ordering (S:159-160)** fails when **a coordinator dispatches `/sc:auggie-review <PR> --unattended` after P1 and before P2**. Trace: flag accepted, default posting stays on, PR comments written. Maps to F-6.
6. I can break this specification by **Accumulation Attack**. The invariant at **WC-10 (S:68)** fails when **a foreground Agent-tool wait lasts 20 minutes**. Trace: no heartbeat can be sent for 20 minutes; Orca's response to heartbeat age is UNVERIFIED (CAPS:182). Maps to F-4.
7. I can break this specification by **Accumulation Attack**. The invariant at **pr-submit row (S:114)** fails when **`--poll-interval` is 300**. Trace: one sleep of at least 300 s exceeds AC-4.3's 240 s. Maps to F-5.
8. I can break this specification by **Divergence Attack** on the status mapping (S:63): a run reports `partial`, the worker sends `--outcome succeeded`, the Task settles completed and dependents become startable on incomplete output. Maps to F-8.

## Guard Condition Boundary Table
Guards identified in the spec: GC-1 `--unattended` switch (D1, WC-2, S:51, S:228); GC-2 output directory known and writable (WC-4, S:62); GC-3 single-wait length rule (WC-10, S:68, S:210); GC-4 status to outcome mapping (WC-5, S:63); GC-5 startup readiness limit (WC-1, S:59); GC-6 nesting depth (WC-8, S:66, S:33). The table is complete: all 6 guards, 6 rows each, every cell populated.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|--------------------|--------|
| GC-1 `--unattended` token | S:51, S:228 | Zero/Empty | no arguments at all | false | Standalone behaviour unchanged (SA-1, S:146) | OK |
| GC-1 | S:51, S:228 | One/Minimal | `--unattended` only, no topic or target | true | Per-command gate rows resolve it as blocked where a required input is missing (tdd S:90, cli-eval S:104); no general rule | OK |
| GC-1 | S:51, S:228 | Typical | `--unattended --output dir/` | true | WC-2 applies; gate rows in section 3 | OK |
| GC-1 | S:83-89, S:128 | Maximum/Overflow | `--unattended --interactive` (adversarial, brainstorm, release-split) | true | Unspecified: only "brief never passes `--interactive`" (F-7) | GAP |
| GC-1 | S:228 | Sentinel Value Match | topic text `"... --unattended ..."` inside quotes | true or false (detection rule absent) | Unspecified token rule (F-7) | GAP |
| GC-1 | S:128 | Legitimate Edge Case | `/sc:git ... --unattended` (coordinator-only command) | true | Unspecified: "get no `--unattended` mode" gives no refusal or ignore rule (F-7) | GAP |
| GC-2 output dir | S:62 | Zero/Empty | no directory passed under `--unattended` | false | Unspecified (F-2) | GAP |
| GC-2 | S:62 | One/Minimal | directory does not exist yet | true | Implied creation: contract "written on every outcome ... before any other output exists" | OK |
| GC-2 | S:62 | Typical | `--output .dev/x/` (adversarial, brainstorm, reflect) | true | Contract at `<dir>/return-contract.yaml` | OK |
| GC-2 | S:87, S:90, S:120 | Maximum/Overflow | `--output` is a file (tdd, init-lite, spec-panel) | undefined | WC-4 names a directory; no rule for a file (F-1) | GAP |
| GC-2 | S:62, S:64, S:73 | Sentinel Value Match | directory already holds `return-contract.yaml` from attempt 1 | true | WC-6 "fresh directory" against a fixed path; no owner named (F-3) | GAP |
| GC-2 | S:62 | Legitimate Edge Case | directory unwritable or inside `.git/` | false | Unspecified; "written on every outcome" cannot hold (F-2) | GAP |
| GC-3 wait length | S:68 | Zero/Empty | no blocking call (0 s) | false | No split needed | OK |
| GC-3 | S:68 | One/Minimal | 1 s call | false | No split needed | OK |
| GC-3 | S:68 | Typical | 60 s call | false | No split needed | OK |
| GC-3 | S:68, S:104, S:114 | Maximum/Overflow | foreground Agent-tool wait of 20 min, cli-eval eval up to 3600 s | true | Split rows exist for cli-eval and pr-submit only; Agent-tool waits unaddressed (F-4) | GAP |
| GC-3 | S:68, S:210 | Sentinel Value Match | exactly 300 s, and 250 s | false (WC-10), true for AC-4.3 | WC-10 allows 250-300 s calls that AC-4.3 rejects (F-5) | GAP |
| GC-3 | S:114 | Legitimate Edge Case | `--poll-interval 300` sleep | true | No cap on the interval (F-5) | GAP |
| GC-4 status mapping | S:63 | Zero/Empty | contract absent or empty | false | `--outcome failed` ("no report exists") | OK |
| GC-4 | S:63 | One/Minimal | `status: succeeded` | true | `--outcome succeeded` | OK |
| GC-4 | S:63, S:263 | Typical | `status: partial` | true | `--outcome succeeded`, body names partial; meaning of partial undefined (F-8) | OK |
| GC-4 | S:63 | Maximum/Overflow | worker sends `worker_done` twice after a retry in the same dispatch | n/a | "exactly once" (WC-5) | OK |
| GC-4 | S:62 | Sentinel Value Match | existing contract `status` with a value outside the four | false | "keep their fields" against "one of four" (F-8) | GAP |
| GC-4 | S:63 | Legitimate Edge Case | audit verdict FAIL | true | `--outcome succeeded`, body states the verdict | OK |
| GC-5 readiness | S:59 | Zero/Empty | no startup prompt (0 s) | true | Passes (CAPS:44-45) | OK |
| GC-5 | S:59 | One/Minimal | startup prompt with 1 s fallback | true | Passes | OK |
| GC-5 | S:59 | Typical | 30 s fallback | true | Passes (EVIDENCE.md:45 via CAPS:49, UNVERIFIED file) | OK |
| GC-5 | S:59 | Maximum/Overflow | fallback of 50 s against a 60 s default | undefined | "well inside" is not quantified | GAP |
| GC-5 | S:44 | Sentinel Value Match | a command's first action is a question | undefined | Asserted harmless, not evidenced (F-9) | GAP |
| GC-5 | S:59 | Legitimate Edge Case | coordinator raises `--timeout-ms` | true | Allowed (CAPS:45) | OK |
| GC-6 nesting | S:66 | Zero/Empty | depth 0 coordinator starts a worker | true | Allowed | OK |
| GC-6 | S:33, S:66 | One/Minimal | depth 1 worker calls `worker-start` | false | Refused `nested_worker_depth_exceeded`; WC-8 forbids the call | OK |
| GC-6 | S:65 | Typical | Agent-tool subagent inside a worker | true | Not an Orca worker, not counted (E4, S:24) | OK |
| GC-6 | S:252 | Maximum/Overflow | depth setting raised (D5 option b) | true | Rejected by D5; WC-8 still forbids command-side calls | OK |
| GC-6 | S:66 | Sentinel Value Match | invalid depth setting | n/a | Orca falls back to 1 (CAPS:100); not a spec concern | OK |
| GC-6 | S:276 | Legitimate Edge Case | depth-1 worker calls `task-create` | unknown | WC-8 forbids it either way; Orca behaviour UNVERIFIED (S:276) | OK |

GAP rows: 13, each carried into a finding (F-1, F-2, F-3, F-4, F-5, F-7, F-8, F-9; the GC-5 "well inside" row is part of F-9).

## Quantity Flow Diagram
The only count-bearing flow in the spec is the command classification and its phase assignment. Counts are checked against the inventories (INV-A:3 = 21, INV-B:3 = 22).

```text
[Commands: 43] --> [Classify: 3.1 ready 10 + 3.2 needs-change 27 + section 4 coordinator-only 6] --> [37 worker-capable, 6 withheld]
                                                              |
                                                              v
                                [Phase assignment, explicit Commands cells]
                                P1: 13 (9 from 3.2 + 4 fixes in 3.1)
                                P2: 15 (11 from 3.2 + 4 from 3.1)
                                P3: 4        P4: 3          => 35 explicit
                                brainstorm, init-lite: no phase cell (small fix "None")  <-- 2 covered only by P1's "every command" sentence (S:159)
                                |
                                v
[Consumer AC-1.1: expects 37 (S:195)]   [Consumer AC-1.2: expects the 13 P1 commands (S:196)]   [Consumer D3(a): pr-submit withheld in practice -> 36 + 1 (S:240)]
```

Consistency check: 43 = 10 + 27 + 6 (S:76) and the row counts in section 3.1 (10), 3.2 (27) and section 4 (6) match; the phase cells add to 35 plus the two commands covered by the P1 sentence. No stage assumes count conservation where it does not hold, so no FR-19 mismatch is raised. Two soft divergences are recorded as N-4 and F-6: AC-1.1 counts 37 while D3(a) removes pr-submit from the worker set, and the P1 Commands cell omits brainstorm and init-lite.

## Expert consensus and disagreement
- Consensus: the decision in section 1 is sound and honestly bounded; the contract-file approach (one shared document, per-command short sections) is the right shape.
- Consensus: the weak points are definitions the spec leaves open (directory, partial, token, per-attempt directory) and a phase plan whose interim state is unsafe.
- Disagreement: Wiegers would grade F-1/F-2 higher because AC-2.2 and 7.2 step 4 cannot be evaluated without a path; Fowler and Nygard hold them at Medium because the parent-directory reading is available. Resolved by the grading sentence (needs a guess), so Medium.

## Follow-up candidates (Medium and minor)
Medium (graded under the brief's grading check; labels shown in brackets):

| ID | Label | Grade | One-line | Spec lines |
|----|-------|-------|----------|-----------|
| F-1 | MAJOR | Medium | File-valued `--output` against WC-4's directory | S:62, S:87, S:90, S:120, S:200 |
| F-2 | MAJOR | Medium | No rule for missing or unusable output directory; research and workflow have no passed directory | S:62, S:92, S:116 |
| F-3 | MAJOR | Medium | "Fresh dir" against a fixed pre-dispatch path; no owner for a new directory per attempt | S:62, S:64, S:73 |
| F-4 | MAJOR | Medium | WC-10 reaches all foreground Agent-tool waits; only two commands handled | S:68, S:104, S:114, S:210 |
| F-5 | MAJOR | Medium | pr-submit `--poll-interval` uncapped; AC-4.3 (240 s) stricter than WC-10 (5 min) | S:68, S:114, S:210 |
| F-6 | MAJOR | Medium | P1 flag on all commands before P2-P4 gates exist; AC-1.1 reaches P4 commands; D3(a) | S:154, S:159-162, S:195, S:240 |
| F-7 | MAJOR | Medium | No token rule for `--unattended`; person-mode flags and coordinator-only commands unspecified | S:83-89, S:128, S:228 |
| F-8 | MAJOR | Medium | Four-value `status` against existing contracts; `partial` undefined | S:62, S:63, S:263 |
| F-9 | MAJOR | Medium | Readiness-order claim stated as fact, not in UNVERIFIED; "well inside" unquantified | S:44, S:59, S:158 |
| F-10 | MAJOR | Medium | AC-0.4 step 3 requires the WC-4 contract path at P0, before it exists | S:62, S:81, S:182, S:194 |
| F-11 | MAJOR | Medium | Concurrent source edits by workers in one worktree not covered | S:69, S:73 |
| F-12 | MAJOR | Medium | Acceptance greps that can pass without detecting the defect (details below) | S:172, S:176, S:193 |
| F-13 | MAJOR | Medium | Missing-contract-file behaviour; AC-C1 against the P0 deliverables | S:52, S:147, S:158, S:172 |
| F-14 | MAJOR | Medium | tasklist `--unattended` to reflect starts auto-remediation | S:88, S:122 |

F-10 detail. AC-0.4 says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1" (S:194), but step 3 still requires the outcome to match "the contract's `status`" and the report path to be "the WC-4 contract path" (S:182). At P0 troubleshoot's only report is REPORT.md and its contract exists only with `--caller task-unified` (INV-B:242). Grading sentence: an implementer who runs AC-0.4 as written cannot satisfy step 3 for troubleshoot, and "a failure here reopens section 1" (S:194); the lenient reading (step 3 also uses the existing file) is available, so Medium. Recommendation: carve out step 3 in the same sentence as step 4.

F-12 detail (demonstrated in the sandbox with `printf ... | grep -E`). (a) The additive-edit checks AC-C5, AC-0.3 and SA-4's test use `grep -E '^-[^-]'` on `git diff -U0` (S:176, S:193). A removed markdown bullet or a removed `---` line appears in the diff as `-- text` or `----`, which that pattern skips: the test input `-- removed bullet`, `-- another removed bullet`, `---`, `-changed prose line` printed only `-changed prose line`. Command files are mostly bullet lists, so deleting or rewriting a bullet passes the check meant to prove edits are additive. (b) In the raw file the pipes inside those commands are written `\|` (S:172, S:176, S:193); pasted as written, the AC-C1 pattern matched nothing (`exit-escaped-pipe-match=1` for the input `orca orchestration ask`) and the pipeline is broken; with plain `|` the same input matched. Grading sentence: an implementer who copies the AC text as written gets a check that cannot fail. Medium, because the rendered table shows the right pipe and the intent is clear. Recommendation: use `grep -E '^-'` minus the `^---` header line (or `git diff --numstat` deleted-count equal to the allowed fixes), and move the commands out of table cells.

Minor notes (never fail the review):
- N-1 Section 1.1 says command changes are "limited to" three things (S:16) while section 3 and SA-4 add defect fixes (S:149, S:220). Reword 1.1.
- N-2 "Ready today" tdd, troubleshoot and release-split still carry stall paths until P2 (S:89-91); the brief constraints in 3.1 name flags but not the `--depth deep` short-input STOP (S:91) or the tasklist-input confirm (S:89).
- N-3 7.2 step 7 gives `worker-release` with no selector (S:186); step 2 uses `worker-show --dispatch`, whose usage is not in the capabilities inventory (CAPS:129 only), so the flag is UNVERIFIED.
- N-4 AC-1.1 requires every section 3.2 command, including `/sc:load`, to name `return-contract.yaml` (S:195), while the load row and the Decisions table say load has no report (S:112, S:265); the P1 Commands cell omits brainstorm and init-lite (S:159).
- N-5 D4 lists auggie-review and task, both P2 commands (S:244, S:160), while S:154 says Phases 1-3 need no user decision; fine under recommendation (a), unresolved under (b).
- N-6 AC-1.3 asks for "a scratch worktree" and `claude -p` (S:197); the repo rule on how worktrees are created is in `CLAUDE.md`, which is not in the workspace, so UNVERIFIED; `claude -p` is also the headless signal reflect keys on (INV-B:109), so a reflect test would differ.
- N-7 Section 4 explains why `/sc:git` is withheld partly by the README ban on commits (S:133, README.md:31), which is a rule for this planning run, not for product behaviour.
- N-8 No coordinator procedure for a worker that dies without `worker_done` or a contract; the Orca guide governs (CAPS:120-129), but section 2.3 could point to it.
- N-9 UNVERIFIED #14 reports an independent check of about 340 citations (S:285); that check is not reproducible from the workspace.
- N-10 E5 and AC-C1 cover commands, skills, agents and core only (S:25, S:172); hooks and templates are not covered.
- N-11 The contract has no version field and the ordering "contract complete before `worker_done` carries its path" is implied only (S:62, S:63); workflow's contract is versioned 1.1 (INV-B:272).

## What I covered
- Read in full: README, spec (all 9 sections plus Decisions and UNVERIFIED), the three inventories. Cross-checked about 60 citations in the spec against the three inventories (`INV-A`/`INV-B` row and note lines, `CAPS` lines, the 43 = 21 + 22 count and the 10 / 27 / 6 split, the phase cell totals, the section 4 six, `INV-A:106` and `INV-B:320` for the citation checks). No contradiction found between a spec citation and the inventory line it points at.
- Not checkable here, so UNVERIFIED: every `src/superclaude/...` line the spec cites directly (S:11 lists 11 it re-read), `CLAUDE.md:*` citations, `.dev/evals/...EVIDENCE.md`, `.dev/codegraph-migration/...`, `orca-ide` guide output, `pyproject.toml:38`, `install_core.py:4,13-24,33`, `Makefile:68-74`, `plugins/superclaude/**`.
- Not covered: the quality of the 37 per-command rows beyond their consistency with the inventories; the actual text of any command or skill; Orca runtime behaviour.
- Not run: no `--fix`, no improved specification (the command forbids it in a first review of this kind and the brief says do not edit the candidate); no second review started.

## Reviser brief
Blocking finding ids: none. Nothing for a reviser to change in this round. Rules for any reviser, restated from the Review Loop: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; the reviser reports the byte size before and after.

verdict: PASS

review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (labelled whole-document audit, first review)

## Header
- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `361193fc0635fb15c8c62bef7845f79c10650c2ce1378fb6cefbbb9b882a7ae8` (285 lines)
- baseline: not given, not needed (first review). Prior report: none.
- reviewer model used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full)
- coverage: whole document, sections 1-9, Decisions and UNVERIFIED items, checked against the requirements the spec states and against the three inventories. Not covered: any file outside `.dev/orca-command-refactor/` (see Evidence limits).

Citation keys: `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`.

## Evidence limits
Only `README.md`, the three inventories and the candidate exist in the workspace. Every citation in the spec to `src/superclaude/...`, `CLAUDE.md`, `.dev/codegraph-migration/...`, `.dev/evals/...`, `Makefile`, `pyproject.toml`, `plugins/...` and Orca's own files could not be opened here. Those are UNVERIFIED by this review; where the spec routes through an inventory line (`INV-*`, `CAPS:*`) I checked that line.

Checked and found as cited: command counts 21 + 22 = 43 (INV-A:3, INV-B:3, SPEC:76) and the 10 / 27 / 6 split (5+5 ready, 13+14 needs-change, 3+3 coordinator-only, INV-A summary and INV-B:285-299); the 10 rows of SPEC:81-92, 27 rows of SPEC:97-125 and 6 rows of SPEC:131-137 match those inventory splits; the phase lists at SPEC:159-163 match the Phase column of section 3.2 (9 + 11 + 4 + 3 = 27 changed commands, plus the P1 and P2 small fixes to ready commands); `CAPS:44-47, 52, 58-80, 86, 92, 97-103, 107-116, 129-130, 145-161, 177-188` say what SPEC:21-39, 59-70, 229, 281-284 attribute to them; `INV-A:14, 36, 60-62, 65-66, 90-98, 106, 113, 118, 120` and `INV-B:272, 285-301, 311, 320, 323` say what the spec attributes to them; `README:6, 12, 30-31, 35` match SPEC:222, 23, 67, 133.

## Hard gate: Guard Condition Boundary Table
Triggered: the spec carries thresholds and guards (wait sizes, readiness limit, confidence floor, nesting depth, outcome mapping, flag detection). Classes left out of a guard are named in its last row. The six input classes are a menu, not a quota.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-10 split rule | SPEC:68 | Zero/Empty | wait of 0 s | no split | not a wait; nothing to specify | OK (class cannot matter) |
| WC-10 split rule | SPEC:68 | Typical | 240 s wait | no split needed | allowed; matches AC-4.3 (SPEC:210) | OK |
| WC-10 split rule | SPEC:68, 210, 266 | Legitimate Edge Case | 280 s single wait (over 4 min, not over 5 min) | WC-10 "longer than 5 minutes": false, so no split | WC-10 allows it; AC-4.3 says "no single tool call exceeds 240 s" and fails it | GAP (see B-2) |
| WC-10 split rule | SPEC:68, 104 | Maximum/Overflow | 3600 s eval (cli-eval) | split into at most 4 min waits | specified | OK |
| WC-1 prelaunch fallback | SPEC:59 | Legitimate Edge Case | fallback of 40 s | "well inside" 60 s: undefined | evidence: 30 s passes, "above about 45 s" fails (SPEC:59); no number is required of an implementer | GAP (M-6) |
| WC-5 outcome mapping | SPEC:63 | Zero/Empty | contract file present but empty, or no `status` key | undefined | only "no report exists" maps to failed; an empty or keyless file is not covered (7.2 step 4 `test -s` and enum check at SPEC:183 cover the checker, not the worker) | GAP (M-5) |
| WC-5 outcome mapping | SPEC:63 | Sentinel Value Match | existing contract whose `status` uses another vocabulary (for example workflow's `status`, INV-B:272) | undefined | "Commands that already write a contract keep their fields" (SPEC:62) while AC step 4 asserts the four-value enum (SPEC:183); workflow gets "None" to change (SPEC:92) | GAP (M-5) |
| Confidence floor, task row | SPEC:121 | Legitimate Edge Case | confidence 0.70 to 0.89 | row blocks only below 0.70 | what `/sc:task` does unattended in the 0.70 to 0.89 band is not stated; the sibling `/sc:agent` prompts there (INV-A:36) | GAP (M-7) |
| `--unattended` detection | SPEC:51, 228 | Sentinel Value Match | the string `--unattended` inside quoted prompt or spec content (a TDD topic, a spec-panel body) | undefined | D1(a) says the flag "cannot misfire"; no rule says only a standalone argument token counts | GAP (M-7) |
| WC-3 `ask` once | SPEC:61 | One/Minimal | command with 3 gates (cli-portify, SPEC:105) | "ask the coordinator once" | whether once per gate or once per run is not stated | GAP (M-4) |
| Nesting depth | SPEC:33, 66 | Typical | depth 1 | worker may not start workers | specified, D5 | OK |
| Retry output dir | SPEC:64 | Sequence (repeat) | `--retry-of` worker reuses a dir that holds attempt 1's `return-contract.yaml` | undefined | WC-4 says "written on every outcome" but nothing forces the file to be removed or stamped at start | GAP (M-3) |
| Phase gate AC-C3 | SPEC:174 | Typical | baseline suite with pre-existing failures | pass if no baseline pass regresses | specified | OK |

Gates satisfied: the table is complete for the guards found; no blank Specified Behavior cell. Each GAP above was graded by the first-review grading check; none except B-2 holds without a further assumption.

## Quantity Flow Diagram (Pipeline Dimensional Analysis, Fowler leads, Whittaker attacks)
Trigger: the rollout is a multi-stage pipeline whose counts change at each stage (SPEC:76, 154-163).

```text
[Source: 43 commands (SPEC:76)] --> [Stage 1: coordinator-only split (SPEC:128-137)] --> [37 worker-capable (43 - 6)]
    |
    v
[Stage 2: ready vs needs-change] --> [10 ready (SPEC:81-92)] + [27 changed (SPEC:97-125)]
    |
    v
[Stage 3: who gets --unattended and a WC-4 contract]
    P1: 8 (analyze, build, business-panel, design, document, explain, index, test)  (SPEC:159, 195)
    P2: 15 (11 changed + reflect, release-split, tdd, troubleshoot)               (SPEC:160)
    P3: 4 (roadmap, validate-roadmap, validate-tests, save)                       (SPEC:161)
    P4: 2 (implement, post-release), +1 pr-submit only under D3(b)                (SPEC:162, 239-242)
    = 29 accept --unattended (30 under D3(b))
    never: 8 = load (usage line only, SPEC:112) + 6 ready commands that get no flag
           (adversarial, brainstorm, cleanup-audit, index-repo, init-lite, workflow) + pr-submit under D3(a)
    |
    v
[Consumers that assume all 37 workers carry a contract]
    WC-4 / WC-5 / 7.2 step 4 (SPEC:62-63, 183)  <-- MISMATCH for the 6 ready commands (see M-1)
    section 2.3 brief template (SPEC:73) tolerates absence of the flag ("where the command's phase has added it")
```

Consistency check result: the spec's own counts reconcile (43 = 37 + 6; 27 = 9 + 11 + 4 + 3; 29 + 8 = 37). The mismatch is behavioral, not arithmetic: finding M-1. Severity under FR-19 would be CRITICAL only if a consumer assumed count conservation with a concrete wrong result; here the consumer assumption is explicit text, graded Medium by the first-review grading check because the worker still has a report file to name.

## === REQUIREMENTS ANALYSIS === (Wiegers lead, Adzic, Cockburn)

### B-1 (MAJOR, blocking, High): AC-C5 passes when a line starting with `-` is deleted
- Expert: Wiegers (testability), Adzic (concrete example).
- Location: SPEC:176 (AC-C5), SPEC:193 (AC-0.3); depends on SA-4 (SPEC:149) and the P0 to P3 rollout.
- Grading sentence: An implementer who follows AC-C5 as written runs `git diff -U0 ... | grep -E '^-[^-]'` and reads empty output as "edits are additive", and that is wrong because a unified-diff line for a deleted Markdown bullet `- item` is `-- item`, whose second character is `-`, so the pattern skips it; the same holds for a deleted `---` frontmatter delimiter or a deleted `--flag` line.
- Concrete example (Adzic): a P2 edit removes the bullet `- Wait for user confirmation` from `cmd/cleanup.md`. The diff line is `-- Wait for user confirmation`. `grep -E '^-[^-]'` prints nothing, AC-C5 passes, and a standalone prompt (SA-1, SPEC:146) is gone.
- Why it is a spec defect: AC-C5 is the only mechanical enforcement of the additive-edit rule SA-4 and the phase pass condition at SPEC:167 ("a phase passes only when every check in its block and every common check passes"). Command files are bullet-heavy, so the blind spot is the common case. AC-0.3 uses the same pattern for `HOW-WE-WORK.md`.
- Recommendation: pass condition should list every deleted line except the `--- a/` file header, for example `grep -E '^-' | grep -vE '^--- '`.

### M-1 (Medium, High): the 6 ready commands that never get `--unattended` have no contract, but WC-4, WC-5 and 7.2 treat every worker as having one
- Expert: Wiegers (traceability), Cockburn (coordinator as primary actor).
- Location: SPEC:62-63 (WC-4, WC-5), SPEC:79 and SPEC:76 versus SPEC:159 and SPEC:195.
- Text conflict: SPEC:79 says the worker reports "the named file until Phase 1 adds the contract", and SPEC:76 says the P1 small fixes "add none". For cleanup-audit, index-repo and init-lite, P1 adds no contract and no later phase does; WC-5 keys the outcome on "the report says failed or blocked", which a Markdown report (`PROJECT_INDEX.md`, `context-audit.md`) cannot say.
- Why Medium: the worker still has a file to name, and the grading check needs a guess (the worker sends `succeeded` when the file exists).
- Recommendation: state, per ready command without a contract, which file `--report-path` names and how WC-5 maps its outcome (for example "file present and non-empty = succeeded"). Or say that P0 only needs a report file for them.

### M-2 (Medium): general rule for nested invocations is missing
- Expert: Wiegers.
- Location: SPEC:51, 122 (tasklist passes `--unattended` to reflect), 90 (tdd nested `/task`), 92 (workflow runs reflect), 84 (brainstorm to adversarial).
- WC-2 forbids prompts "under `--unattended`" but only the tasklist row says the flag propagates. tdd, brainstorm and workflow call other skills (INV-B:52, INV-A:35) and no row says whether the callee gets `--unattended`. Requirement never stated, so Medium.

### M-3 (Medium): stale contract after a retry or resume
- Expert: Nygard (failure modes), Whittaker (sequence attack).
- Location: SPEC:62 (WC-4 "written on every outcome"), SPEC:64 (WC-6 resume or fresh dir).
- Attack: attempt 1 writes `status: blocked` to `<output-dir>/return-contract.yaml`. A `--retry-of` worker with a resume flag reuses that directory and crashes before writing. The coordinator opens the old file, which reads `blocked` and has a valid enum, and 7.2 step 4 (SPEC:183) passes it. Nothing requires removing the file at start or stamping it with a run id.
- Medium because the text states a requirement the document never made (a freshness rule). Recommendation: a `started_at` or dispatch-id field, or delete-at-start.

### M-4 (Medium): WC-3 conflicts with D2(a) and WC-9, and its terms are loose
- Expert: Nygard, Whittaker (divergence attack).
- Location: SPEC:61 (WC-3), SPEC:67 (WC-9), SPEC:233-236 (D2), SPEC:245 (D4), SPEC:114 (pr-submit row "the worker may use `ask`").
- WC-3 lets a worker with a preamble `ask` the coordinator and "re-invoke or resume the command with the answer as a flag". (1) For `/sc:implement`, the only accepted Ruling is the person's, and "another agent's message" is not (SPEC:233, citing qa.md:238); D2(a) says the worker ends `failed`. WC-3 does not exclude implement. (2) WC-9 says outward actions turn on "only through the command's own explicit flag written in the brief" (SPEC:67); an `ask` answer that adds `--post-pr` after launch is not in the brief, and D4(a) wants the user's instruction quoted in the brief. (3) Section 3 names no answer flag for any gate, and many gates resume as "fresh dir" (SPEC:100-125), where re-invocation redoes the work. (4) "ask the coordinator once" is not defined per gate or per run (table row above).
- Each reading needs a guess that the implementer picks the worse reading, so Medium. Recommendation: say WC-3 does not apply to implement Rulings and outward authorizations (they follow D2 and D4), and name the answer flag where a command has one.

### M-5 (Medium): status vocabulary of existing contracts is not checked
- Expert: Wiegers, Adzic.
- Location: SPEC:62 ("keep their fields"), SPEC:183 (enum assertion), SPEC:92 (workflow "None"), SPEC:262 (Decisions, "fixed four-value set").
- The inventories record the existence of workflow's, brainstorm's and reflect's contracts, not their `status` values (INV-B:272, INV-B:112). If workflow's `status` is another word, the unchanged workflow fails the 7.2 enum check at P0. Not verifiable here (`refs/return-contract.md` is outside the workspace), so UNVERIFIED; Medium.

### M-6 (Medium): WC-1 has no number and no test
- Expert: Wiegers (measurability).
- Location: SPEC:59, 167-187.
- "well inside the readiness limit" is quantified only by the evidence column (30 s passes, about 45 s fails). No AC checks WC-1 beyond 7.2 step 1 `state: ready`. An implementer picks any value from 31 to 44 s.

### M-7 (Medium): two unspecified edge inputs
- Expert: Whittaker (zero/empty and sentinel-collision attacks).
- (a) Confidence band 0.70 to 0.89 for `/sc:task` unattended: SPEC:121 covers only below 0.70; `/sc:agent` prompts in that band (INV-A:36). (b) `--unattended` appearing inside quoted content: SPEC:51 and D1(a) (SPEC:228) say the flag "cannot misfire on a person" but give no rule that only a standalone argument token counts.

### M-8 (Medium): AC-1.1 and AC-1.4 cannot stay true or cannot fail
- Expert: Crispin-style testability note under Wiegers.
- AC-1.1 (SPEC:195) asserts that "no other command ... has one [section] yet". The same test file persists into P2, and AC-C3 (SPEC:174) forbids a baseline pass from failing, so the P1 assertion breaks when P2 adds sections unless it is phase-scoped; SPEC:199 says only that P2 "gains" assertions. AC-1.4 (SPEC:198) greps `return-contract.yaml` in the adversarial skill; INV-A:60 shows the skill already names the contract at `:427`, so the grep prints matches before any edit and "names one fixed path" has no mechanical pass condition.

### M-9 (Medium): WC-11 is stated as a universal "never" but three ready commands write fixed paths
- Expert: Nygard.
- Location: SPEC:69 versus SPEC:85-87.
- index-repo writes `PROJECT_INDEX.md` with no output flag (INV-A:53); cleanup-audit's output dir is fixed (SPEC:85 admits "one audit per worktree at a time"); init-lite's default is a fixed path (SPEC:87). Two workers on one of these in one worktree write the same file. The spec's fix is a coordinator rule in prose for cleanup-audit only.

## === ARCHITECTURE ANALYSIS === (Fowler lead, Newman, Hohpe, Nygard)

Assessment of the decision itself: sound and well-evidenced. Orca above, commands as units of work, a single shared contract file, no Orca calls in commands (SPEC:16, 29-39, 213). The rejected alternative is argued from Orca's own depth limit and standalone use (`CAPS:97-103, 145-149`), and the spec states the weak spot honestly: no direct-route run exists, so P0 smoke runs come first (SPEC:43, 158). Interface segregation is good: one coordinator-side brief (2.3), one command-side section, and the six orchestrating commands kept out (SPEC:128-139). Nothing found that contradicts SA-1 to SA-6 as written, apart from the points below.

- A-1 (Medium, Newman): the contract has no version field. `return-contract.yaml` is consumed by a coordinator across independently changed commands (SPEC:62); workflow's file carries a contract version ("contract 1.1", INV-B:272) while the WC-4 field list does not. A later field change breaks old coordinators silently. Follow-up candidate.
- A-2 (Medium, Nygard): AC-C1 (SPEC:172) greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent`, while P0 adds an Orca section to `HOW-WE-WORK.md` and a brief template to `WORKER-CONTRACT.md` (SPEC:158) and SA-2 allows an Orca mention in the contract file (SPEC:147). A natural Orca section that names `orca-ide orchestration ...` fails AC-C1 on a stated deliverable. Whether it fails depends on wording, so Medium. Also, the pattern is written with `\|` for the table; copied raw it matches the literal string `orchestration|worktree|...` and passes vacuously (note N-2).
- A-3 (Medium, Hohpe): the 29-versus-8 split of `--unattended` is correct but the coordinator brief template (SPEC:73) is the only place the split is made usable; section 2.3 should list which commands accept the flag at which phase, or the brief will carry a flag a command rejects. This is a documentation gap, not a wrong outcome.
- A-4 (note, Fowler): `partial` maps to `succeeded` (SPEC:63, 263). The consequence for retry (a coordinator that treats `succeeded` as done) is accepted in the Decisions row; the first-sentence rule keeps it visible. No finding.
- A-5 (note, Nygard): the stall failure mode (a worker waiting on a prompt shows as healthy, `CAPS:52, 129`) is handled by WC-2 plus 7.2 step 2, which polls `agentWait` once per 5 minutes. A prompt that ends the turn (a chat offer, not a tool call) may not set `agentWait`; SPEC:44 and 60 flag that case in prose but 7.2 step 5 (transcript search for `AskUserQuestion`) does not detect it. Follow-up candidate.

### B-2 (MAJOR, blocking, High): WC-10 and AC-4.3 set different limits for one wait
- Expert: Nygard (operational), Whittaker (divergence attack: boundary between two branches).
- Location: SPEC:68 (WC-10), SPEC:114 (pr-submit row), SPEC:210 (AC-4.3), SPEC:266 (Decisions: "4 minutes leaves a margin").
- Grading sentence: An implementer who follows WC-10 as written builds a poll wait of 280 s (it does not block "for longer than 5 minutes", so no split is required), and that is wrong because AC-4.3 requires "no single tool call exceeds 240 s" and fails it, and the Decisions row shows the intended limit is always 4 minutes.
- Concrete attack: pr-submit's poll-plus-sleep iteration takes 4 min 40 s. WC-10: allowed. SPEC:114 tells the implementer to "confirm each single iteration ... stays under 4 minutes", which agrees with AC-4.3 but not with WC-10's trigger. Two stated texts disagree on the 240 to 300 s band.
- Applies when D3(b) is chosen (AC-4.3) and, for the cli-eval P2 change (SPEC:104), to the split size; the contradiction is in the requirement text itself, whichever D3 answer is given.
- Recommendation: make WC-10's trigger "any single tool call that could exceed 4 minutes" so that it equals AC-4.3, or lift AC-4.3 to 5 minutes.

## Minor notes
- N-1: SPEC:159 says "the eight no-gate commands", but three of them have an explicit refusal (`business-panel --mode socratic`, `explain --format interactive`, `test --watch`, SPEC:102, 108, 123). They are no-gate in the WC-2 sense (no prompt), so the wording only needs "no default-on prompt".
- N-2: the `\|` in AC-C1 (SPEC:172) is correct only when the table is rendered.
- N-3: SPEC:140 labels pr-submit "a worker candidate" yet it is counted in the 27 and in P4 (SPEC:114, 162), although the recommended D3(a) makes no change to it. The count line at SPEC:76 should say "27, of which pr-submit is conditional".
- N-4: citations that point to files outside the workspace (see Evidence limits) carry line numbers I could not open. SPEC:11 itself says only 11 of them were re-read by the spec author on 2026-11-02.

## Expert consensus
- Wiegers, Adzic, Cockburn: requirements are mostly measurable, each row has an evidence column and an AC; the defects are in how checks are written (B-1, B-2, M-8) and in scope gaps for commands without a flag (M-1).
- Fowler, Newman, Hohpe, Nygard: architecture is coherent and conservative; the open points are lifecycle and versioning of the contract file (M-3, A-1) and the interaction of `ask` with D2 and D4 (M-4).
- Disagreement: none recorded between the experts.

## Follow-up candidates
Medium (warnings, never trigger a revision): M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, A-1, A-2, A-3, A-5.
Minor notes: N-1, N-2, N-3, N-4, A-4.
This run is non-interactive in the sandbox, so the question "open an issue for these?" is not asked here; no issue was created. The session that owns the loop asks the user once.

## Reviser brief
Blocking finding ids: B-1, B-2.

Restated contract (the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding, and report the byte size before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings alone. A brief may not widen this scope or regrade a minor or Medium finding as blocking, and this brief overrides no clause.

- B-1: SPEC:176 and SPEC:193 only (the two `grep -E '^-[^-]'` pass conditions).
- B-2: SPEC:68 (WC-10 trigger), or SPEC:210 (AC-4.3 limit), whichever is narrower; SPEC:114 and SPEC:266 already agree with 240 s.

verdict: FAIL

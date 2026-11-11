review: 1 of 3

# Spec panel report (critique mode): orca-worker-contract-spec.md

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`. Run: first review of the full document, `baseline: missing` not applicable (no `--re-review`).
- Command line reviewed: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`.
- Citation shorthand: `spec:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`.
- Evidence rule: the three inventories and the README are the only evidence this review could open. Every source line the candidate cites under `src/`, `.dev/evals/`, `.dev/codegraph-migration/`, `CLAUDE.md`, `~/.claude`, `/opt/Orca` or an Orca guide is UNVERIFIED here; where a finding leans on one, it is reached through the inventory line that quotes it.

## What this review covered

- Read in full: the candidate (sections 1-9, Decisions, UNVERIFIED items), `inventory/commands-a.md` (120 lines), `inventory/commands-b.md` (323 lines), `inventory/orca-capabilities.md` (188 lines), `README.md`.
- Checked: the 43 / 10 / 27 / 6 arithmetic against both inventories; the command-to-phase assignment (all 37 worker-capable commands traced to a phase); every WC-n requirement against the section 3 rows and the section 7 checks; the section 5 standalone rules against section 3; the Decisions table against the inventories.
- Experts that reviewed, in the fixed order: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. Under `--focus requirements,architecture` the lead panels are Wiegers/Adzic/Cockburn and Fowler/Newman/Hohpe/Nygard; Whittaker is active in every panel.
- Not covered: the source files and Orca guides behind the section 3 citations (not openable in this sandbox); the live repository; `EVIDENCE.md`; git history. `--focus correctness` is not active, so no State Variable Registry is produced.

## Precedence note

Review Loop bullet 2 calls FR-8/FR-9 findings blocking. The brief's grading check narrows blocking to findings whose "stated text as written builds X, and X is wrong because Y" sentence holds with no further assumption, and sends a requirement the document never states to follow-up candidates "even when its label is MAJOR". This report applies the brief (Review Loop bullet 7 lets a brief narrow, never widen). Guard-table GAP rows therefore keep their FR-8 MAJOR label but are graded by the brief's sentence test; each one that fails the test points to a Medium finding below.

## Mandatory artifact 1: Guard Condition Boundary Table

Triggered: the candidate states thresholds and conditional rules (WC-1, WC-5, WC-10, the task confidence rule, the `--unattended` switch, the output directory). The table is complete before synthesis (FR-10). Construction Nygard, completeness Crispin, attack Whittaker. Guards are the ones the candidate itself states.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| GC-1 wait-split | spec:68 (WC-10) | Zero/Empty | longest blocking call = 0 s | false | nothing to split; nothing to heartbeat | OK |
| GC-1 wait-split | spec:68 | One/Minimal | 1 s | false | no split | OK |
| GC-1 wait-split | spec:68 | Typical | 3 min | false | no split; next heartbeat due at 5 min | OK |
| GC-1 wait-split | spec:68 | Maximum/Overflow | one Agent-tool fan-out call running 20 min, or a 3600 s eval (INV-A:65) | true | polls and evals: split into waits of at most 4 min; an Agent-tool call cannot be split and the text names no behavior for it | GAP (F-11) |
| GC-1 wait-split | spec:68, spec:266 | Sentinel Value Match | exactly 300 s, and a 4.5 min call that starts 1 min after the last heartbeat | false | ">5 minutes" is not met, so no split, yet the heartbeat falls due inside the call | GAP (minor, N-05) |
| GC-1 wait-split | spec:61 (WC-3) | Legitimate Edge Case | worker blocked inside `ask` or `check --wait` | n/a | heartbeat skipped; the block is a liveness signal (CAPS:64) | OK |
| GC-2 pre-ready prompt | spec:59 (WC-1) | Zero/Empty | no prompt in the launch path | false | worker reaches `input_accepted` | OK |
| GC-2 pre-ready prompt | spec:59 | One/Minimal | prompt with 1 s fallback | true | falls back inside the limit | OK |
| GC-2 pre-ready prompt | spec:59 | Typical | prompt with 30 s fallback | true | passes, 34 s start (CAPS:49) | OK |
| GC-2 pre-ready prompt | spec:59 | Maximum/Overflow | fallback above about 45 s | true | fails at `agent_readiness` (CAPS:49); the rule says only "well inside" the limit and gives no number | GAP (N-04) |
| GC-2 pre-ready prompt | spec:59 | Sentinel Value Match | coordinator raises `--timeout-ms` for one start (CAPS:45) | true | the allowed fallback bound for that start is not restated | GAP (N-04) |
| GC-2 pre-ready prompt | spec:59 | Legitimate Edge Case | trust or update dialog, not a command prompt (CAPS:50) | true | Orca pre-accepts Claude trust (CAPS:50); other dialogs are outside the contract | OK |
| GC-3 task confidence | spec:121 | Zero/Empty | confidence 0 | true | blocked | OK |
| GC-3 task confidence | spec:121 | One/Minimal | confidence 0.01 | true | blocked | OK |
| GC-3 task confidence | spec:121 | Typical | confidence 0.85 | false | proceeds as today (INV-B:199 quotes only the below-0.70 prompt) | OK |
| GC-3 task confidence | spec:121 | Maximum/Overflow | confidence 1.0 | false | proceeds | OK |
| GC-3 task confidence | spec:121 | Sentinel Value Match | exactly 0.70 | false | "below 0.70" is strict; INV-B:199 quotes "< 0.70" | OK |
| GC-3 task confidence | spec:121 | Legitimate Edge Case | confidence cannot be computed (null) | n/a | nothing stated | GAP (F-04 area, minor N-06) |
| GC-4 outcome rule | spec:63 (WC-5) | Zero/Empty | no report file, or a 0-byte file | true / unknown | no file: `failed`; empty or unparsable file: not stated | GAP (F-03) |
| GC-4 outcome rule | spec:63 | One/Minimal | report containing only `status: succeeded` | false | `succeeded` | OK |
| GC-4 outcome rule | spec:63 | Typical | `succeeded` or `partial` | false | `--outcome succeeded` | OK |
| GC-4 outcome rule | spec:63, spec:62 | Maximum/Overflow | report `status` outside the four-value set (an older command vocabulary kept under "keep their fields") | unknown | nothing stated | GAP (F-13) |
| GC-4 outcome rule | spec:63, spec:262 | Sentinel Value Match | `status: blocked`, which is also an Orca Task status (CAPS:89) | true | mapped to `--outcome failed`; stated | OK |
| GC-4 outcome rule | spec:63 | Legitimate Edge Case | stale report left by an earlier attempt in the same directory, new attempt wrote nothing | false (wrongly) | "no report exists" is true only for a clean directory | GAP (F-03) |
| GC-5 output directory | spec:62, spec:73 | Zero/Empty | `--output` absent or empty under `--unattended` | n/a | nothing stated | GAP (F-07) |
| GC-5 output directory | spec:62 | One/Minimal | `--output .` | n/a | contract lands at repo root; not stated, inferrable | OK |
| GC-5 output directory | spec:62 | Typical | valid new directory | n/a | `<output-dir>/return-contract.yaml` | OK |
| GC-5 output directory | spec:62 | Maximum/Overflow | unwritable directory, or one inside `.git/` or a distributable `.claude/` folder | n/a | nothing stated | GAP (F-07) |
| GC-5 output directory | spec:62, spec:90, spec:87 | Sentinel Value Match | `--output` is a file path (tdd, init-lite) | n/a | `<output-dir>` is undefined for a file | GAP (F-02) |
| GC-5 output directory | spec:62, spec:64 | Legitimate Edge Case | directory already holds a `return-contract.yaml` | n/a | nothing stated | GAP (F-03) |
| GC-6 unattended switch | spec:60, spec:146 | Zero/Empty | flag absent | false | today's behavior (SA-1) | OK |
| GC-6 unattended switch | spec:60 | One/Minimal | flag present, no other flags | true | gates resolve per section 3 | OK |
| GC-6 unattended switch | spec:60, spec:228 | Typical | flag plus the gate flags section 3 lists | true | per row | OK |
| GC-6 unattended switch | spec:159 | Maximum/Overflow | flag passed to a gated command before its P2/P4 conversion | true | accepted; gate behavior in the interval not stated | GAP (F-09) |
| GC-6 unattended switch | spec:228 | Sentinel Value Match | the token `--unattended` appears inside quoted prompt text | ambiguous | "cannot misfire on a person" is claimed; token parsing is not defined | GAP (N-07) |
| GC-6 unattended switch | spec:100, spec:103, spec:110, spec:118 | Legitimate Edge Case | `--unattended` together with `--interactive` | true | refused for cleanup, improve, roadmap, explain-interactive, auggie; no general rule for the rest | GAP (N-07) |

## Mandatory artifact 2: Quantity Flow Diagram (Pipeline Dimensional Analysis)

Triggered: the rollout is a multi-stage partition of a command set where counts change at each stage. Fowler annotates; Whittaker attacks the divergence.

```text
[Source: 43 commands (INV-A:3 = 21, INV-B:3 = 22)]
   --> [Stage 1: verdict split, spec:76]
   --> [10 ready (spec:81-92)] + [27 needs change (spec:97-125)] + [6 coordinator-only (spec:130-136)] = 43   (conserved)
   --> [Stage 2: worker-capable = 10 + 27 = 37]
   --> [Stage 3: phase assignment, spec:156-162]
         P1 Commands column = 13 | P2 = 15 | P3 = 4 | P4 = 3  => 35 listed
         unlisted in any Commands column: brainstorm, init-lite (both "None", spec:84, spec:87)   => 37
   --> [Consumer A: AC-1.1 expects `## Unattended mode` in 37 commands at the end of P1, spec:195]
   --> [Consumer B: P1 Commands column edits 13, spec:159]  <-- MISMATCH (37 vs 13), softened only by the P1 scope sentence "every command in sections 3.1 and 3.2"
   --> [Consumer C: AC-1.2 runs the live check on "each P1 command", incl. load, spec:196, spec:159]  <-- load has no contract, spec:112
```

Divergence is recorded in F-01 (the load contradiction needs no reading choice) and F-09 (the other 22 commands rely on a reading).

## Synthesis (critique mode, grouped by bucket)

### === REQUIREMENTS ANALYSIS ===

**F-01** CRITICAL, **blocking**. Expert: Wiegers (traceability), attack: Whittaker (Divergence).
- Issue: AC-1.1 and AC-1.2 cannot pass for `/sc:load`, which the same document says gets no report file and no `## Unattended mode` section.
- Grading sentence: An implementer who follows the stated `/sc:load` row (spec:112: report "none", "use it as a step inside another worker's brief, not as its own Task", phase "P1 (usage line only)") and the Decisions row (spec:265: "a report file would be an unrequested addition. Only its usage-line defect is fixed") builds a P1 that changes load's Usage line and nothing else, and that build is wrong because AC-1.1 (spec:195) asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` (load is a row of section 3.2), and AC-1.2 (spec:196) runs the live check, whose step 4 requires a contract file (spec:183), on "each P1 command" with load named in the P1 row (spec:159). Two stated texts contradict each other; an implementer who adds the section to satisfy the check builds the contract the Decisions row rejects.
- Supporting, not needed for the grade: P1's Commands column lists 13 commands (spec:159) while AC-1.1 tests 37; the P1 scope sentence covers the gap for most commands. For `/sc:pr-submit`, AC-1.1 forces a P1 section although spec:139 and spec:240 keep it a worker candidate only if decision D3 accepts that.
- Recommendation: make AC-1.1 and AC-1.2 name the same command set as the section 3 phase column for P1, and state load's exemption in both.
- Priority: High. Quality impact: Consistency +2, Testability +1.

**F-02** MAJOR label, graded **Medium**. Expert: Wiegers (clarity), Adzic (example), attack: Whittaker (Sentinel Collision).
- Issue: the contract location rule `<output-dir>/return-contract.yaml` (spec:62) does not fit the commands whose output is a file or an auto-derived directory.
- Grading sentence: An implementer who follows WC-4 as written builds the contract at the directory the coordinator passed, and that is wrong for tdd and init-lite (`--output <file>`, spec:87, spec:90), adversarial (`<output>/adversarial/`, spec:83), workflow (`.dev/tasks/to-do/<id>/`, spec:92) and implement (beside the ledger, spec:109), if the implementer picks the reading where the row overrides WC-4. The text allows either reading, so the grade needs a guess.
- Also unstated: where workflow writes the contract for a pre-creation STOP, when no package id or directory exists yet (spec:92; INV-B:272 says pre-creation STOPs write none today); how the path is "known before dispatch" (spec:73) when the id or slug is derived at run time. AC-2.2 (spec:200) runs tdd with `--output <file>` and expects a contract with `blocked_question`, but names no path for step 4 (spec:183).
- Recommendation: one sentence in WC-4 that says whether a per-command location overrides the general rule, and a fixed location for file-valued `--output` commands.
- Priority: Medium. Quality impact: Clarity +1, Testability +1.

**F-03** MAJOR label, graded **Medium**. Expert: Adzic (scenario), attack: Whittaker (Sequence).
- Issue: retry and re-run behavior leaves the first attempt's output and the "no report exists" test unreliable.
- Grading sentence: An implementer who follows WC-6 (spec:64: "writes each run into a fresh output directory") together with WC-4 (spec:62: contract at exactly the directory passed) builds a command that either overwrites the passed directory or invents a sub-directory, and the first is wrong because it destroys the first attempt's output, the second because it breaks the known contract path; which one is wrong depends on a guess about who creates the fresh directory, since the "Command" owner column (spec:64) and the coordinator brief (spec:73, no new-directory-per-retry rule) both leave it open.
- Concrete attack: attempt 1 writes `<dir>/return-contract.yaml` with `status: succeeded`; attempt 2 (`--retry-of`, same brief) stops before writing anything. WC-5 (spec:63) sends `--outcome failed` only when "no report exists"; the stale file exists, so the worker reports `succeeded` over a failed run. About 20 rows say "fresh dir" (spec:99-125), and the commands that do have a resume flag (roadmap, implement, tdd, pr-submit, brainstorm) have no stated behavior when a retry brief omits it; AC-3.2 (spec:205) requires "starts fresh" in a directory that already holds `.session-memory.md`, without saying whether existing artifacts are kept. No check in section 7 runs `--retry-of`.
- Recommendation: state that a contract is deleted or its `run_id`/timestamp checked before WC-5 reads it, and who supplies the fresh directory.
- Priority: Medium. Quality impact: Testability +1, Completeness +1.

**F-04** MAJOR label, graded **Medium**. Expert: Cockburn (actor and goal), Wiegers.
- Issue: the flags that authorize outward actions are not named for the commands that need them.
- Grading sentence: An implementer who follows WC-9 (spec:67: an outward default "turns on only through the command's own explicit flag written in the brief") builds explicit flags for post-release's VM, install, commit and PR (spec:113), task's `commit`/`push` (spec:121) and pr-submit (spec:114), and the document names none of them; the implementer picks a flag name per command, so the grade needs a guess. For auggie-review the row says `--unattended` implies `--no-post-pr` and "posting returns only with an explicit `--post-pr`" (spec:100), but the inventory shows only the negative form `--no-post-pr` (INV-A:38) and the row lists "Other required change: none", so a new positive flag and its precedence over the implied negative are both undefined.
- Recommendation: name each authorizing flag (or say it is added in P4 with D4) and the precedence rule.
- Priority: Medium. Quality impact: Completeness +1.

**F-05** MAJOR label, graded **Medium**. Expert: Cockburn, Crispin (acceptance).
- Issue: cli-portify has three approval gates that all resolve as "blocked", and no flag carries an approval.
- Grading sentence: An implementer who follows the cli-portify row (spec:105) builds a command that blocks at the first gate and a `--resume <contract>` flag that restarts at `resume_phase`, and that is wrong if resuming re-presents the same gate (so AC-2.3, spec:201, "happy-path run ... with every required flag" can never finish), or right if resume counts as approval; the row does not say which, so the grade needs a guess. The third gate ("approval before delivering", INV-A:45) sits after the last resume point.
- The cli-eval row (spec:104) requires "the safety flags" without naming the set.
- Recommendation: say whether resuming at a gate counts as approval, or add an approval flag.
- Priority: Medium. Quality impact: Completeness +1.

**F-06** MAJOR label, graded **Medium**. Expert: Wiegers (state assumptions), Nygard.
- Issue: the tasklist row is accepted on an unverified nesting assumption, and one of its stops has no resolution.
- Grading sentence: An implementer who follows the tasklist row (spec:122: "none" beyond passing `--unattended` to each reflect) builds Stage 10.5 as it is today with reflect headless, and that is wrong if nested spawning does not work or if reflect's `needs_human_decision` HALT (INV-B:209) is reached; the first depends on facts INV-B:210 and INV-B:322 mark UNVERIFIED and the second on a stop the row never names, so the grade needs a guess.
- The row states the fan-out "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`", while INV-B:215 recommends running the per-phase reflect at the worker's top level, and the Decisions row (spec:268) says nothing read contradicts a verdict. Under the headless rule remediation is auto-accepted (INV-B:109), so a tasklist worker would also run corrective hand-offs; the row does not say so.
- Recommendation: list the HALT as a blocked resolution, and cite why the INV-B recommendation was not followed.
- Priority: Medium. Quality impact: Completeness +1.

**F-07** MAJOR label (FR-9 area), graded **Medium**. Expert: Whittaker (Zero/Empty).
- Issue: no behavior for a missing, unwritable or forbidden output directory.
- Grading sentence: This is a requirement the document never states: WC-4 (spec:62) says the contract is written "on every outcome", and §2.3 (spec:73) puts the directory on the coordinator, but if the brief omits `--output`, or the directory cannot be written, the command cannot write the contract it must write. The text does not cause harm; it leaves the state undefined.
- Recommendation: one rule: refuse before any work and print the refusal in chat, or fall back to a named default directory.
- Priority: Medium. Quality impact: Completeness +1.

**F-08** MAJOR label, graded **Medium**. Expert: Crispin (acceptance), Gregory.
- Issue: several requirements have no acceptance check, and two checks can pass wrongly.
- Grading sentence: Not a stated text that does harm; missing and weak criteria.
  - No check covers WC-3 (ask path), WC-6 (`--retry-of`), WC-10 for cli-eval (the only wait-size check is AC-4.3 for pr-submit, spec:210), WC-9 for task's commit/push, or WC-11 beyond `/sc:save` (AC-3.4, spec:207).
  - AC-2.4 (spec:202) compares `gh api .../reviews --jq length` and `.../comments --jq length` before and after; without `--paginate` each call returns at most one page (default 30 items, UNVERIFIED here), so a PR with 30 or more comments shows an unchanged count after a post.
  - 7.2 step 2 asks for `worker-show` at least every 5 minutes while step 3 blocks on `check --wait --timeout-ms 900000` (15 min) (spec:181-182), so both cannot hold in sequence.
  - AC-4.2 (spec:209) says "no new PR" without a baseline list.
  - AC-C1 (spec:172) greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent`, while SA-2 (spec:147) allows an Orca example inside the contract file and the P0 plan adds an Orca section to the routing guide (spec:158); a lowercase literal in either file fails the check. The markdown-escaped `\|` also needs unescaping before the command runs.
- Recommendation: add the missing checks; add `--paginate`; fix the 7.2 step order; state the literal form allowed in core files.
- Priority: Medium. Quality impact: Testability +2.

### === ARCHITECTURE ANALYSIS ===

**F-09** MAJOR label, graded **Medium**. Expert: Fowler (interface), Nygard (failure modes).
- Issue: the interval between P1 and P2/P4 leaves `--unattended` accepted and not honored on gated commands.
- Grading sentence: An implementer who follows the P1 row (spec:159: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)") builds the flag on auggie-review, task, post-release and pr-submit with no behavior change, and that is wrong because the P0 brief template (spec:158) and §2.3 (spec:73) tell the coordinator to pass `--unattended`, so until P2/P4 an auggie-review worker still posts to GitHub by default (INV-A:38) and a task worker still prompts or commits; the parenthetical can be read as limiting the no-op to no-gate commands, which leaves the gated ones unspecified, so the grade needs a guess.
- Recommendation: until a command's gate rows land, make the flag refuse (exit with a blocked contract) instead of silently doing nothing.
- Priority: Medium. Quality impact: Consistency +1.

**F-10** MAJOR label, graded **Medium**. Expert: Newman (service boundaries), Hohpe (message flow).
- Issue: no rule says whether `--unattended` propagates into commands or skills a command calls.
- Grading sentence: This is a requirement the document never states. Only tasklist-to-reflect is handled (spec:122). Not handled: tasklist Stage 9 calling `sc:task --compliance strict` (INV-B:46, INV-B:211), whose confidence and TFEP gates (INV-B:199) are then reachable inside the worker; cli-eval create calling `/sc:spec-panel` and `sc:adversarial` (INV-A:44); release-split calling brainstorm and adversarial (INV-B:121); roadmap calling `sc:save` (INV-B:154). Any one of these can stall the worker without `worker_done`.
- Recommendation: add one WC rule that a nested call inherits `--unattended`, then check each call site named above.
- Priority: Medium. Quality impact: Completeness +1.

**F-11** MAJOR label, graded **Medium**. Expert: Nygard (liveness), attack: Whittaker (Accumulation).
- Issue: WC-10 splits waits for polls and evals but is silent on Agent-tool fan-out, which is also a single blocking tool call.
- Grading sentence: An implementer who follows WC-10 (spec:68: "a command step that blocks a single tool call for longer than 5 minutes ... must be split") builds splitting for pr-submit polls and cli-eval, and for the ready commands that run 8 to 10 parallel agents (cleanup-audit INV-A:42, adversarial INV-A:35, tdd INV-B:47) builds nothing, because an Agent-tool call cannot be cut into 4-minute pieces; whether those commands are then "ready" under WC-10 depends on reading the rule as limited to its two examples (a poll, a long eval), so the grade needs a guess. Heartbeat age is not known to feed liveness (CAPS:130, UNVERIFIED), which lowers the harm.
- Recommendation: state that WC-10 covers polls and sleeps only, and what a worker does during a long Agent-tool call.
- Priority: Medium. Quality impact: Clarity +1.

**F-12** MAJOR label, graded **Medium**. Expert: Fowler (shared state), attack: Whittaker (Divergence).
- Issue: WC-11 says two workers in one worktree "must never write the same file", but the ready rows and roadmap keep shared paths.
- Grading sentence: An implementer who follows WC-11 (spec:69) builds timestamped or slug-based default paths, and the cleanup-audit row (spec:85: fixed `.claude-audit/`, "one audit per worktree at a time"), index-repo (fixed `PROJECT_INDEX.md`, INV-A:53) and init-lite (fixed default, INV-A:55) keep fixed paths, so the "must never" in WC-11 is met only by coordinator discipline; the roadmap row (spec:118) does not mention that roadmap calls `sc:save` at every wave (INV-B:154), which writes the single-owner keys WC-11 says are not written. Either reading is allowed, so the grade needs a guess.
- Recommendation: restate WC-11 as a coordinator rule where a path is fixed, and add `sc:save` to the roadmap row.
- Priority: Medium. Quality impact: Consistency +1.

**F-13** MAJOR label, graded **Medium**. Expert: Newman (versioning), Hohpe.
- Issue: the shared contract adds fields to existing contracts with no version marker or vocabulary check.
- Grading sentence: An implementer who follows WC-4 (spec:62: existing contracts "keep their fields and add the missing ones") and the Decisions row (spec:262: fixed four-value `status`) builds one validator (spec:183) for contracts that already have their own `status` values and a version (workflow's is "contract 1.1", INV-B:272); the inventories do not list those values, so whether the old values fit the four-value set is UNVERIFIED and the grade needs a guess.
- Recommendation: add a `contract_version` field and check the old status values in P0.
- Priority: Medium. Quality impact: Consistency +1.

### === MINOR NOTES (never fail the review) ===

- N-01: §1.1 (spec:16) says command changes are "limited to the worker contract", while section 3 and SA-4 (spec:149) add defect fixes (roadmap, validate-roadmap, validate-tests, explain tools, business-panel frontmatter, adversarial filename).
- N-02: spec:154 says "Phases 1-3 need no user decision", while D1 (`--unattended` selection) and D4 (outward authorization) touch P1 and P2 rows (spec:100, spec:121, spec:228, spec:244).
- N-03: E3 (spec:23) cites `invocation_method: "skill-direct"` as evidence the direct route works, while §1.4 (1) (spec:43) says the PR #329 run used an Agent-tool subagent and proves "the nested route, not the direct route".
- N-04: WC-1 gives no numeric fallback bound (spec:59) and no phase or check owns the launch setup beyond 7.2 step 1.
- N-05: WC-10 uses ">5 minutes" for the split and "4 minutes" for the wait (spec:68, spec:266); a call of 4 to 5 minutes is neither.
- N-06: the task row (spec:121) has no rule for a confidence value that cannot be computed.
- N-07: `--unattended` token parsing in quoted text and flag conflicts with `--interactive` have no general rule (spec:228; per-row refusals only).
- N-08: the claim "The 43 commands in `cmd/`" (spec:76) rests on the two enumerated scope lists (INV-A:3, INV-B:3), not a directory listing. UNVERIFIED here: this session's installed skill list also names `sc:graph`, `sc:impact` and `sc:issue`, which appear in neither inventory; the worktree's `cmd/` was not opened.
- N-09: WC-3 allows "ask the coordinator once" (spec:61); cli-portify has three gates, and the text does not say whether it is once per gate or once per run.
- N-10: the word `blocked` is used for the contract status and is also an Orca Task status (CAPS:89); WC-5 maps it, so no wrong outcome follows, but the coordinator brief template should keep the two apart.
- N-11: spec-panel's row (spec:120) needs a new `--target-release` flag as well as `--output` and lists "Other required change: none".

## Adversarial analysis (Whittaker, FR-3 format)

1. I can break this specification by **Sequence Attack**. The invariant at **WC-5 / WC-6 (spec:63-64)** fails when **a retry attempt writes no contract and a stale one remains**. Concrete attack: before: `<dir>/return-contract.yaml` = `status: succeeded` (attempt 1). Attempt 2 stops at an early STOP and writes nothing. After: the file still exists, "no report exists" is false, the worker sends `--outcome succeeded`. Severity: MAJOR label (F-03, Medium).
2. I can break this specification by **Divergence Attack**. The invariant at **WC-4 vs the section 3 rows (spec:62, spec:83-92)** fails when **the passed `--output` is a file, or the command nests its own sub-directory**. Concrete attack: `/sc:tdd "<component>" --unattended --output docs/x/TDD_X.md`: `<output-dir>` is undefined; the coordinator opens `docs/x/TDD_X.md/return-contract.yaml` and finds nothing. Severity: MAJOR label (F-02, Medium).
3. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 / §2.3 (spec:62, spec:73)** fails when **the brief omits `--output`**. Concrete attack: before: no directory; after: the command has no place for the contract it must always write, and no refusal path exists. Severity: MAJOR label (F-07, Medium).
4. I can break this specification by **Accumulation Attack**. The invariant at **WC-10 (spec:68)** fails when **a command makes one blocking Agent-tool call longer than 5 minutes**. Concrete attack: a 20 minute 8-agent cleanup-audit wave; no heartbeat is possible; the rule names no behavior. Severity: MAJOR label (F-11, Medium).
5. I can break this specification by **Sequence Attack**. The invariant at **P1 / AC-1.1 (spec:159, spec:195)** fails when **P1 is built from its own Commands column**. Concrete attack: the 13 listed commands are edited; AC-1.1 tests 37 and load, which gets no section, fails. Severity: CRITICAL (F-01, blocking).
6. Sentinel Collision, Zero/Empty on `--unattended` parsing: no finding above minor (N-07, N-10).

## Quality metrics (0-10)

Clarity 7, Completeness 6, Testability 6, Consistency 5. Panel consensus: the decision (Orca coordinates, commands stay units of work) is well supported by the inventories (spec:21-39, INV-A:95, INV-B:306) and the 43 / 10 / 27 / 6 split reconciles with both inventories. The defects are in the acceptance section and in places where the general rule (WC-4, WC-6, WC-10, WC-11) meets a per-command row. Disagreement: Newman and Hohpe would grade F-10 higher than Medium; Wiegers and Crispin hold it at Medium because the text does not state it.

## Follow-up candidates (Medium and minor; none fails this review)

Medium: F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-11, F-12, F-13.
Minor: N-01 to N-11.

## Open blocking findings

F-01 (CRITICAL, open).

## Reviser brief

Applies to blocking finding ids only: **F-01**.
- Revise only text a blocking finding names (here: AC-1.1 at spec:195, AC-1.2 at spec:196, and, if the reviser prefers, the `/sc:load` row at spec:112).
- Add no rule, mechanism or section that no blocking finding calls for; the Medium findings above are not to be fixed in this cycle.
- Each added paragraph or table cites its finding id.
- The reviser reports the byte size of the specification before and after the change.
- The reviser reads this report, not the command.

verdict: FAIL
